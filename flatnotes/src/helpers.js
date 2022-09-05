export function getSearchParam(paramName) {
  let urlSearchParams = new URLSearchParams(window.location.search);
  return urlSearchParams.get(paramName);
}

export function setSearchParam(paramName, value) {
  let url = new URL(window.location.href);
  let urlSearchParams = new URLSearchParams(url.search);
  urlSearchParams.set(paramName, value);
  url.search = urlSearchParams.toString();
  window.history.replaceState({}, "", url.toString());
}
