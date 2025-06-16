export const handleFetch = async ({ event, request, fetch }) => {
  if (request.url.startsWith(event.url.origin)) {
    // même origine, on ajoute le header Authorization du contexte
    const token = event.request.headers.get('Authorization');
    if (token) request.headers.set('Authorization', token);
  }
  return fetch(request);
};