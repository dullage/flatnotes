export function getToastOptions(title, description, isFailure = false) {
  return {
    summary: title,
    detail: description,
    severity: isFailure ? "error" : "success",
    closable: false,
    life: 5000,
  };
}

export function getUnknownServerErrorToastOptions() {
  return getToastOptions(
    "Unknown Error",
    "Unknown error communicating with the server. Please try again.",
    true,
  );
}
