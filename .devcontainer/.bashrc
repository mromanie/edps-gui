port=7860
repo_name=$(basename $GITHUB_REPOSITORY)
echo Start the GUI at: https://${CODESPACE_NAME}-${port}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/${repo_name}
