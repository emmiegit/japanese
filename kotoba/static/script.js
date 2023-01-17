function request(method, route, data, callback) {
  fetch(route, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(callback);
}

function nextCard() {
  request('GET', '/card/next', null, function(response) {
    // TODO
  });
}

function answer(cardId, action) {
  request('POST', '/card/answer', { cardId, action }, function(response) {
    // TODO
  });
}

// TODO setup page
