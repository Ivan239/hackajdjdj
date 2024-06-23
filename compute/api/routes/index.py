import logging
import tempfile
from fastapi import APIRouter, HTTPException
import requests

from .models.video import SingleVideo

from ..xpocketbase import client
from pocketbase.utils import ClientResponseError
from moviepy.editor import VideoFileClip
import librosa

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
async def probe_with_audio(
    video_id: str,
    moderation_session_id: str
):
#     try:
#         db_response = client.collection('videos').get_one(video_id)
#     except ClientResponseError as e:
#         api_logger.error(f"POST /video: {e.status} {e.data}")
#         raise HTTPException(status_code=e.status, detail=e.data)

#     if not db_response:
#         raise HTTPException(status_code=404, detail="Video not found")
    
#     try:
#         api_logger.log(logging.INFO, f"video_id='{db_response.id}'")
#         probe = client.collection('video_probs').get_list(
#             query_params={
#                 'filter': f"video_id~'{db_response.id}'"
#             }
#         )
#     except ClientResponseError as e:
#         api_logger.error(f"GET /video_probs: {e.status} {e.data}")
#         pass
    
#     if len(probe.items) > 0:
#         return {
#             "video": db_response,
#             "violations": probe.items
#         }
    
#     file = client.get_file_url(db_response, db_response.video_file, {})
    
#     points = video_flow.probe(
#         video_link=file,
#     )
    
#     from ..audio.audio_detect import Recognizer, PBManager
#     pbman = PBManager()
#     pbman.set_collections('fingerprints', 'records')
#     recognizer = Recognizer(pbman)
    
#     with tempfile.NamedTemporaryFile('wb', suffix='.mp4') as tf:
#         tf.write(requests.get(file).content)
#         tf.seek(0)
#         with VideoFileClip(tf.name) as clip:
#             with tempfile.NamedTemporaryFile('wb', suffix='.wav') as file:
#                 clip.audio.write_audiofile(file.name, fps=16000)
#                 file.seek(0)
                
        
                
#                 outputs = []
#                 for point in points.to_dict(orient='records'):
#                     res_ = client.collection('videos').get_list(query_params={
#                         'filter': f"video_file~'{point['video_name']}'"
#                     })
#                     results = recognizer.recognize_file(
#                         file.name,
#                         int(point['start'] / db_response.fps),
#                         int(point['end'] / db_response.fps)
#                     )
#                     if len(res_.items) == 0:
#                         continue
#                     res_ = res_.items[0]

#                     if results[0]['record_id'] == res_.id:
#                         originalStart = results[0]['offset_sec']
#                         originalEnd = results[0]['offset_sec'] + (point['end'] - point['start']) / db_response.fps
#                     else:
#                         continue
                    
#                     outputs.append(client.collection('video_probs').create(body_params={
#                         "video_id": res_.id,
#                         "start": point['start'] / db_response.fps,
#                         "end": point['end'] / db_response.fps,
#                         "originalStart": originalStart,
#                         "originalEnd": originalEnd
#                     }))
                
#                 return {
#                     "video": db_response,
#                     "violations": outputs
#                 }
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