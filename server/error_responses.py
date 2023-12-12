from fastapi.responses import JSONResponse

filename_exists_response = JSONResponse(
    content={"message": "The specified filename already exists."},
    status_code=409,
)

invalid_filename_response = JSONResponse(
    content={"message": "The specified filename contains invalid characters."},
    status_code=400,
)

note_not_found_response = JSONResponse(
    content={"message": "The specified note cannot be found."}, status_code=404
)
