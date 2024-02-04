export function getSearchParam(paramName, defaultValue = null) {
  let urlSearchParams = new URLSearchParams(window.location.search);
  let paramValue = urlSearchParams.get(paramName);
  if (paramValue != null) {
    return paramValue;
  } else {
    return defaultValue;
  }
}

export function getSearchParamBool(paramName, defaultValue = null) {
  let paramValue = getSearchParam(paramName)
  if (paramValue == null) {
    return defaultValue
  }
  let paramValueLowerCase = paramValue.toLowerCase();
  if (paramValueLowerCase == "true") {
    return true;
  } else if (paramValueLowerCase == "false") {
    return false;
  } else {
    return defaultValue;
  }
}

export function getSearchParamInt(paramName, defaultValue = null) {
  let paramValue = getSearchParam(paramName)
  if (paramValue == null) {
    return defaultValue
  }
  let paramValueInt = parseInt(paramValue);
  if (!isNaN(paramValueInt)) {
    return paramValueInt;
  } else {
    return defaultValue;
  }
}

export function setSearchParam(paramName, value) {
  let url = new URL(window.location.href);
  let urlSearchParams = new URLSearchParams(url.search);
  urlSearchParams.set(paramName, value);
  url.search = urlSearchParams.toString();
  window.history.replaceState({}, "", url.toString());
}
