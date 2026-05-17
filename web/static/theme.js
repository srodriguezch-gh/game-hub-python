// Theme JS - handles player selection persistence and game state

(function() {
  const PLAYER_KEY = 'gamehub_player';

  function getPlayer() {
    return localStorage.getItem(PLAYER_KEY) || 'Dad';
  }

  function setPlayer(name) {
    localStorage.setItem(PLAYER_KEY, name);
    if (window.socket && name) {
      window.socket.emit('login', name);
    }
  }

  window.gameHub = {
    getPlayer,
    setPlayer,
  };
})();