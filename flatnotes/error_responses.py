from fastapi.responses import JSONResponse

file_exists_response = JSONResponse(
    content={"message": "The specified filename already exists."},
    status_code=409,
)

filename_contains_path_response = JSONResponse(
    content={
        "message": "The specified filename contains path information which is forbidden."
    },
    status_code=403,
)

file_not_found_response = JSONResponse(
    content={"message": "The specified file cannot be found."}, status_code=404
)
