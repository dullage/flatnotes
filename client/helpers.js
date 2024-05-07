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

export function setDarkThemeOn(save = true) {
  document.body.classList.add("dark");
  if (save) localStorage.setItem("darkTheme", "true");
}

export function setDarkThemeOff(save = true) {
  document.body.classList.remove("dark");
  if (save) localStorage.setItem("darkTheme", "false");
}

export function toggleTheme() {
  document.body.classList.contains("dark")
    ? setDarkThemeOff()
    : setDarkThemeOn();
}

export function loadTheme() {
  const storedTheme = localStorage.getItem("darkTheme");
  if (storedTheme === "true") {
    setDarkThemeOn();
  } else if (
    storedTheme === null &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    setDarkThemeOn(false);
  }
}
