from fastapi.responses import JSONResponse

title_exists_response = JSONResponse(
    content={"message": "The specified title already exists."},
    status_code=409,
)

invalid_title_response = JSONResponse(
    content={"message": "The specified title contains invalid characters."},
    status_code=400,
)

note_not_found_response = JSONResponse(
    content={"message": "The specified note cannot be found."}, status_code=404
)
