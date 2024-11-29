echo "Lint for python code"
ruff format streamlit_advanced_audio/

echo "Lint for typescript code"
cd streamlit_advanced_audio/frontend
npm run format