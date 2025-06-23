import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import graphviz
import panel as pn
import param
import pypdf
import requests
from panel.viewable import Viewer, Viewable

import fitz
import io
from PIL import Image as PILImage
import os

from edpsgui import pipeline_by_workflow
from .edps_ctl import get_edps

NO_WORKFLOW_MSG = "No workflow"


class WorkflowGraphManager:
    def __init__(self, workflow):
        self.workflow = workflow
        self.merged_filename = f'{workflow}_merged.pdf'

    def create(self):
        graph = get_edps().get_detailed_graph(self.workflow)
        graphviz.Source(graph).render(self.workflow, format='pdf', cleanup=True)
        return self

    def merge(self):
        Path(self.merged_filename).unlink(missing_ok=True)
        files = [Path(f'{self.workflow}.pdf')] + sorted(Path().glob(f'{self.workflow}.[0-9].pdf'), reverse=True)
        merger = pypdf.PdfWriter()
        for file in files:
            merger.append(file.name)
        merger.write(self.merged_filename)
        merger.close()

        return self.merged_filename


class Workflow(Viewer):
    edps_status = param.Boolean(default=None, allow_refs=True)
    workflow = param.String(default=None, allow_refs=True)

    def __init__(self, **params):
        super().__init__(**params)
        self.edps = get_edps()
        self.logger = logging.getLogger('Workflow')
        self.pipeline_documentation_urls = self.get_pipeline_documentation_urls()

    def get_pipeline_documentation_urls(self):
        url = 'https://www.eso.org/sci/software/pipe_aem_table.html'
        pipeline_manual_pattern = r'https://ftp\.eso\.org/pub/dfs/pipelines/instruments/[^/]+/[^/]+-pipeline-manual-[^"\s]+\.pdf'
        reflex_tutorial_pattern = r'https://ftp\.eso\.org/pub/dfs/pipelines/instruments/[^/]+/[^/]+-reflex-tutorial-[^"\s]+\.pdf'
        try:
            response = requests.get(url)
            response.raise_for_status()
            pipeline_manual_urls = re.findall(pipeline_manual_pattern, response.text)
            reflex_tutorial_urls = re.findall(reflex_tutorial_pattern, response.text)
            return pipeline_manual_urls + reflex_tutorial_urls
        except requests.RequestException as e:
            self.logger.error("Failed to fetch URL: %s", e)
            return []

    @staticmethod
    def get_pdf_url(filename) -> str:
        o = urlparse(pn.state.location.href)
        return f'{o.scheme}://{o.netloc}/pdf?file={filename}'

    @pn.depends('workflow')
    async def detailed_graph(self):
        if not self.workflow:
            yield NO_WORKFLOW_MSG
            return
        while True:
            yield pn.indicators.LoadingSpinner(value=True, size=40,
                                               name=f"Creating graph for workflow {self.workflow}...")
            try:
                filename = WorkflowGraphManager(self.workflow).create().merge()
                
                doc = fitz.open(filename, filetype='pdf')
                images = self.convert_pdf(doc)

                # Clean up the temporary PDF files
                files = [Path(f'{self.workflow}.pdf')] + sorted(Path().glob(f'{self.workflow}.[0-9].pdf'), reverse=True)
                for file in files:
                    os.remove(file)
                os.remove(filename)

                width_slider = pn.widgets.IntSlider(name='Width', start=1000, end=2000, value=1000)
                height_slider = pn.widgets.IntSlider(name='Height', start=300, end=1600, value=550)

                def create_images_column(width, height):
                    """
                    Create a scrollable column of PDF page images with preserved aspect ratios.
                    """
                    #if not images:
                    #    return pn.Column(width=width, height=height, scroll=True, margin=(0, 0, 0, 0))
    
                    max_image_width = width - 50
    
                    for page_container in images:
                        if isinstance(page_container, pn.Column) and len(page_container.objects) > 1:
                            img_pane = page_container.objects[1]
                            # Remove the page label (first object)
                            page_container.objects = [img_pane]

                            if isinstance(img_pane, pn.pane.Image):
                                # Get original dimensions if available
                                try:
                                    # Try to get original image dimensions
                                    if hasattr(img_pane, 'object') and img_pane.object is not None:
                                        if hasattr(img_pane.object, 'size'):
                                            orig_width, orig_height = img_pane.object.size
                                        elif isinstance(img_pane.object, str):  # file path
                                            with PILImage.open(img_pane.object) as img:
                                                orig_width, orig_height = img.size
                                        else:
                                            # Fallback to current dimensions
                                            orig_width = img_pane.width or 800
                                            orig_height = img_pane.height or 600
                        
                                        # Calculate proportional height
                                        aspect_ratio = orig_height / orig_width
                                        new_height = int(max_image_width * aspect_ratio)
                        
                                        img_pane.width = max_image_width
                                        img_pane.height = new_height
                        
                                        # CRITICAL: Set the container height to accommodate the image + label
                                        label_height = 30  # Approximate height for "Page X" label
                                        container_padding = 10  # Some internal padding
                                        ###total_container_height = new_height + label_height + container_padding
                                        total_container_height = new_height + container_padding

                                        # Set explicit height for the container
                                        page_container.height = total_container_height
                                        page_container.sizing_mode = 'fixed'
                        
                                except Exception as e:
                                    print(f"Error calculating dimensions: {e}")
                                    # Fallback: use a reasonable default
                                    img_pane.width = max_image_width
                                    img_pane.height = int(max_image_width * 1.4)
                                    page_container.height = int(max_image_width * 1.4) + 40
                                    page_container.sizing_mode = 'fixed'
        
                        # Add margin between containers
                        page_container.margin = (0, 0, 10, 0)
    
                    return pn.Column(*images, width=width, height=height, scroll=True, margin=(0, 0, 0, 0))


                # Bind the function to the sliders
                dynamic_images_column = pn.bind(create_images_column, width_slider, height_slider)

                yield pn.Column(
                    pn.Row(width_slider, height_slider),
                    dynamic_images_column,
                    margin=(0, 0, 0, 0)
                )
                return
            
            except Exception as e:
                yield f"Failed to create graph for workflow {self.workflow} ... {e}"
                return


    def convert_pdf(self, doc):
        images = []
        for page_num in range(len(doc)):
            page =  doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # 1.5x zoom for better quality
            img_data = pix.tobytes("png")

            # Convert to PIL Image for Panel
            pil_img = PILImage.open(io.BytesIO(img_data))

            # Create Panel pane with page label
            img_pane = pn.pane.Image(pil_img, width=800)
            page_label = pn.pane.Markdown(f"**Page {page_num + 1}**")

            images.append(pn.Column(page_label, img_pane))

        doc.close()
        return images

    @pn.depends('workflow')
    def simple_graph(self):
        if not self.workflow:
            return NO_WORKFLOW_MSG
        try:
            graph = get_edps().get_simple_graph(self.workflow)
            filename = f'{self.workflow}_simple'
            url = self.get_pdf_url(f'{filename}.pdf')
    
            #graphviz.Source(graph).render(filename, format='pdf', cleanup=True)
            #doc = fitz.open(f'/home/user/{filename}.pdf')

            pdf_data = graphviz.Source(graph).pipe(format='pdf')
            doc = fitz.open(stream=pdf_data, filetype="pdf")
           
            images = self.convert_pdf(doc)

            width_slider = pn.widgets.IntSlider(name='Width', start=1000, end=2000, value=1500)
            height_slider = pn.widgets.IntSlider(name='Height', start=300, end=1600, value=550)

            def create_images_column(width, height):
                # Calculate height per page (accounting for labels and padding)
                total_pages = len(images)
                label_height = 5  # Approximate height for page labels
                padding = 10  # Some padding
                available_height = max(150, (height - (total_pages * label_height) - padding) // total_pages)
        
                # Update each image width and height to fit within the container
                for page_container in images:
                    if isinstance(page_container, pn.Column) and len(page_container.objects) > 1:
                        img_pane = page_container.objects[1]  # Second object is the image
                        # Remove the page label (first object)
                        page_container.objects = [img_pane]

                        if isinstance(img_pane, pn.pane.Image):
                            img_pane.width = width - 50  # Subtract padding for scrollbar
                            img_pane.height = available_height  # Set height to fit
        
                return pn.Column(*images, width=width, height=height, scroll=True, margin=(0, 0, 0, 0))
    
            # Bind the function to the sliders
            dynamic_images_column = pn.bind(create_images_column, width_slider, height_slider)
    
            return pn.Column(
                pn.Row(width_slider, height_slider),
                dynamic_images_column,
                margin=(0, 0, 0, 0)
            )

        except Exception as e:
            return f"Failed to create graph for workflow {self.workflow}: {e}"

    @pn.depends('workflow')
    def pipeline_documentation(self):
        if not self.workflow:
            return NO_WORKFLOW_MSG
        workflow = self.workflow.split('.')[0]
        pipeline = pipeline_by_workflow.get(workflow, workflow)
        urls = [url for url in self.pipeline_documentation_urls if pipeline in url]

        # Create HTML links that open in new window
        links = [pn.pane.HTML(f'<a href="{url}" target="_blank">{Path(url).name}</a>')
                 for url in urls]
        return pn.Column(*links) if links else "No documentation found"

    @pn.depends('workflow')
    def association_map(self):
        if not self.workflow:
            return NO_WORKFLOW_MSG
        return pn.pane.Markdown(self.edps.get_assoc_map(self.workflow), renderer='markdown', height=800)

    @staticmethod
    def file_content(filename) -> str:
        with open(filename) as f:
            return f.read()

    @pn.depends('workflow')
    def code_viewer(self):
        if not self.workflow:
            return NO_WORKFLOW_MSG
        workflow_path = Path(self.edps.get_workflow_path(self.workflow))
        # workflow_files = {f.name: str(f.resolve()) for f in workflow_path.iterdir() if f.is_file()}
        workflow_files = [f.resolve() for f in workflow_path.iterdir() if f.is_file()]
        workflow_name = self.workflow.split(".")[1] + ".py"
        try:
            selected_file = next(f for f in workflow_files if f.name == workflow_name)
        except StopIteration:
            selected_file = None
        file_selector = pn.widgets.Select(name='Select file', options=workflow_files, value=selected_file)
        code_editor = pn.widgets.CodeEditor(
            value=pn.bind(self.file_content, file_selector),
            language='python', readonly=True, sizing_mode='stretch_both'
        )
        return pn.Column(file_selector, code_editor)

    def __panel__(self) -> Viewable:
        return pn.layout.Tabs(
            ('Task dependencies', self.detailed_graph),
            ('Dataflow', self.simple_graph),
            ('Data sources', pn.Row(self.association_map, sizing_mode='stretch_width', scroll=True)),
            ('Documentation', self.pipeline_documentation),
            ('Code', self.code_viewer),
        )
