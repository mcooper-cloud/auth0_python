function addCountry(user, context, callback) {
  if (context.request.geoip) {
    context.idToken['https://example.com/geoip'] =
      context.request.geoip;
    context.idToken['https://example.com/country'] =
      context.request.geoip.country_name;
    context.idToken['https://example.com/timezone'] =
      context.request.geoip.time_zone;
  }
  callback(null, user, context);
}