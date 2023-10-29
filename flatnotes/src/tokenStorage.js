const tokenStorageKey = "token";

function getCookieString(token) {
  return `${tokenStorageKey}=${token}; path=${window.flatnotesRootPath}/attachments; SameSite=Strict`;
}

export function setToken(token, persist = false) {
  document.cookie = getCookieString(token);
  sessionStorage.setItem(tokenStorageKey, token);
  if (persist === true) {
    localStorage.setItem(tokenStorageKey, token);
  }
}

export function getToken() {
  return sessionStorage.getItem(tokenStorageKey);
}

export function loadToken() {
  const token = localStorage.getItem(tokenStorageKey);
  if (token != null) {
    setToken(token, false);
  }
}

export function clearToken() {
  sessionStorage.removeItem(tokenStorageKey);
  localStorage.removeItem(tokenStorageKey);
  document.cookie =
    getCookieString() + "; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}
