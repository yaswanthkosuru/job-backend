from rest_framework.views import APIView, Response
from langchain_community.document_loaders import PyPDFLoader
from django.shortcuts import get_object_or_404
from users.models import Candidate
import requests
from tempfile import NamedTemporaryFile
import os
from llm.llm_models import groq_lama_model
from llm.templates import summary_template

def process_drive(url):
    # Extract file ID from Google Drive URL
    file_id = url.split('/')[-2]
    # Convert to direct download URL
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    # Download the file
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Save to temporary file
        with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Load and process the PDF
        try:
            loader = PyPDFLoader(temp_file_path)
            pages = loader.load()
            all_page_texts = [page.page_content for page in pages]
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return all_page_texts
        except Exception as e:
            os.unlink(temp_file_path)
            raise Exception(f"Failed to process PDF: {str(e)}")
        
    except requests.RequestException as e:
        raise Exception(f"Failed to download resume file: {str(e)}")
class GenerateCandidateSummaryAPIView(APIView):
    def get(self, request):
        candidate_id = request.GET.get('candidate_id')

        if candidate_id is None:
            return Response({"error": "candidate_id is required"}, status=400)
        
        try:
            candidate = get_object_or_404(Candidate, id=candidate_id)
            resume_file_url = candidate.resume_file_url
            
            if not resume_file_url:
                return Response({"error": "No resume file URL found for this candidate"}, status=404)
            
            try:
                if 'drive.google.com' in resume_file_url:
                    all_page_texts = process_drive(resume_file_url)[0]
                    chain=summary_template | groq_lama_model
                    response = chain.invoke({"input": all_page_texts})
                    result=response.content
                    return Response({"summary": result})
                else:
                    return Response({"error": "Unsupported file type"}, status=400)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)