// Audio feedback for game events
const sounds = {
  move: new Audio('/static/sounds/move.mp3'),
  capture: new Audio('/static/sounds/capture.mp3'),
  check: new Audio('/static/sounds/check.mp3'),
  game_over: new Audio('/static/sounds/game_over.mp3'),
};

const soundMap = {
  move: 'move',
  eat: 'capture',
  click: 'move',
  win: 'check',
  lose: 'game_over',
};

export default function playSound(name) {
  const key = soundMap[name] || name;
  const audio = sounds[key];
  if (audio) {
    audio.currentTime = 0;
    audio.play().catch(() => {});
  }
}