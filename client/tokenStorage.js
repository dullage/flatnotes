const tokenStorageKey = "token";

function getCookieString(token) {
  return `${tokenStorageKey}=${token}; SameSite=Strict`;
}

export function storeToken(token, persist = false) {
  document.cookie = getCookieString(token);
  sessionStorage.setItem(tokenStorageKey, token);
  if (persist === true) {
    localStorage.setItem(tokenStorageKey, token);
  }
}

export function getStoredToken() {
  return sessionStorage.getItem(tokenStorageKey);
}

export function loadStoredToken() {
  const token = localStorage.getItem(tokenStorageKey);
  if (token != null) {
    storeToken(token, false);
  }
}

export function clearStoredToken() {
  sessionStorage.removeItem(tokenStorageKey);
  localStorage.removeItem(tokenStorageKey);
  document.cookie =
    getCookieString() + "; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}
