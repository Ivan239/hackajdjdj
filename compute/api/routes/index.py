import logging
import tempfile
from fastapi import APIRouter, HTTPException
import requests

from ..schema.audio.dataset import Dataset

from .models.video import SingleVideo

from ..xpocketbase import client
from ..audio.audio_detect import Recognizer

from pocketbase.utils import ClientResponseError
from moviepy.editor import VideoFileClip

router = APIRouter(tags=["Video Indexing"])
api_logger = logging.getLogger('uvicorn')


@router.post("/run_index/")
async def index_video(
    video_id: str,
) -> SingleVideo:
    """Create video and audio embeddings for a video.
    
    Args:
        video_id (str): The id of the video to be indexed.
        
    Returns:
        dict: The embeddings for the video.
    """
    try:
        db_response = client.collection('videos').get_one(video_id)
    except ClientResponseError as e:
        api_logger.error(f"POST /video: {e.status} {e.data}")
        raise HTTPException(status_code=e.status, detail=e.data)

    if not db_response:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_response = client.collection('videos').update(
        video_id,
        body_params={
            "video_indexed": True
        }
    )
    
    return []

@router.post("/run_audio_index/")
async def index_audio(
    video_id: str,
) -> SingleVideo:
    """Create video and audio embeddings for a video.
    
    Args:
        video_id (str): The id of the video to be indexed.
        
    Returns:
        dict: The embeddings for the video.
    """
    try:
        db_response = client.collection('videos').get_one(video_id)
    except ClientResponseError as e:
        api_logger.error(f"POST /video: {e.status} {e.data}")
        raise HTTPException(status_code=e.status, detail=e.data)

    if not db_response:
        raise HTTPException(status_code=404, detail="Video not found")
    
    recognizer = Recognizer()
    file = client.get_file_url(db_response, db_response.video_file, {})
    
    recognizer.upload_record(Dataset(record_id=db_response.id, filename=file))
    
    db_response = client.collection('videos').update(
        video_id,
        body_params={
            "audio_indexed": True
        }
    )
    
    return db_response
    
@router.post("/run_check/")
async def probe_video(
    video_id: str,
    moderation_session_id: str
) -> SingleVideo:
    """Check the video for any violations. """
    try:
        db_response = client.collection('videos').get_one(video_id)
    except ClientResponseError as e:
        api_logger.error(f"POST /video: {e.status} {e.data}")
        raise HTTPException(status_code=e.status, detail=e.data)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_response = client.collection('videos').update(
        video_id,
        body_params={
            "checked": True
        }
    )
    
    return db_response
    
@router.post("/run_audio_check/")
async def run_audio_check(
    video_id: str,
    moderation_session_id: str
):
    try:
        db_response = client.collection('videos').get_one(video_id)
    except ClientResponseError as e:
        api_logger.error(f"POST /video: {e.status} {e.data}")
        raise HTTPException(status_code=e.status, detail=e.data)

    if not db_response:
        raise HTTPException(status_code=404, detail="Video not found")
    
    file = client.get_file_url(db_response, db_response.video_file, {})
    
    recognizer = Recognizer()
    
    with tempfile.NamedTemporaryFile('wb', suffix='.mp4') as tf:
        tf.write(requests.get(file).content)
        tf.seek(0)
        with VideoFileClip(tf.name) as clip:
            with tempfile.NamedTemporaryFile('wb', suffix='.wav') as file:
                clip.audio.write_audiofile(file.name, fps=16000)
                file.seek(0)
                
                results = recognizer.recognize_file(
                    file.name,
                    0,
                    int(clip.duration)
                )
                return results
    return 0

@router.post("/run_full_check/")
async def run_full_check(
    video_id: str,
    moderation_session_id: str
):
    """Check the video for any violations. """
    return 0


@router.post("/index_full")
async def index_full(
    video_id: str,
    moderation_session_id: str
):
    """Check the video for any violations. """
    return 0