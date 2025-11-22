// echosense-frontend/src/avatar.js
import { processYoutube } from "./api.js";

const lottieContainer = document.getElementById("lottieContainer");
let currentAnimation = null;
let lottiePlayer = null;

// Load and play a lottie animation file (located in anims/ folder)
export function playLottieAnim(filename, loop=false) {
  // stop existing
  if (lottiePlayer) {
    lottiePlayer.destroy();
    lottiePlayer = null;
  }
  const path = `./src/anims/${filename}.json`;
  lottiePlayer = lottie.loadAnimation({
    container: lottieContainer,
    renderer: 'svg',
    loop: loop,
    autoplay: true,
    path: path
  });
}

// Play the returned sign_sequence sequentially
export async function playSequence(sequence) {
  if (!sequence || sequence.length === 0) {
    // show idle
    playLottieAnim("idle", true);
    return;
  }
  for (const item of sequence) {
    const animFile = item.animation || "idle";
    // try to play file
    playLottieAnim(animFile, false);
    const dur = (item.duration && item.duration > 0) ? item.duration : 1000;
    // lottie durations vary; use duration in seconds *1000 or fallback to 1200ms
    await new Promise(r => setTimeout(r, (dur*1000) || 1200));
  }
  // loop idle at end
  playLottieAnim("idle", true);
}

// High-level handler called by UI
export async function onLoadAndProcessClick(url, videoFrame, transcriptEl) {
  try {
    // show video immediately
    const videoId = extractVideoId(url);
    if (videoId) {
      videoFrame.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    }
    // call backend to download/process
    const res = await processYoutube(url);
    transcriptEl.innerText = "Transcription: " + (res.transcription || "");
    // sequence: array of {word, animation, duration}
    await playSequence(res.sign_sequence || []);
  } catch (err) {
    console.error(err);
    transcriptEl.innerText = "Error: " + err.message;
  }
}

// helper to extract id
export function extractVideoId(url) {
  if (!url) return null;
  if (url.includes("youtu.be/")) {
    return url.split("youtu.be/")[1].split(/[?&]/)[0];
  } else if (url.includes("watch?v=")) {
    return url.split("watch?v=")[1].split(/[?&]/)[0];
  } else {
    return null;
  }
}

// wire UI
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("youtubeInput");
  const btn = document.querySelector("button");
  const videoFrame = document.getElementById("videoFrame");
  const transcriptEl = document.getElementById("transcript");

  btn.onclick = () => {
    const url = input.value.trim();
    onLoadAndProcessClick(url, videoFrame, transcriptEl);
  };

  // start idle animation
  playLottieAnim("idle", true);
});
