export function getSearchParam(paramName) {
  let urlSearchParams = new URLSearchParams(window.location.search);
  return urlSearchParams.get(paramName);
}
