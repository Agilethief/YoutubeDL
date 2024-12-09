console.log("Javascript loaded");
let downloadInterval;
DisplayPreDownload();

const downloadForm =
  document.getElementById("downloadForm");

const progressMessage = document.getElementById(
  "progressMessage"
);
const progressNumber = document.getElementById(
  "progressNumber"
);
const downloadLink =
  document.getElementById("downloadLink");

downloadForm.addEventListener("submit", function (e) {
  e.preventDefault();

  console.log("Form submitted");

  downloadVideo();
});

async function downloadVideo() {
  console.log("Downloading video");
  const videoUrl =
    document.getElementById("id_videourl").value;
  const downloadType = document.getElementById(
    "id_downloadtype"
  ).value;
  const quality =
    document.getElementById("id_quality").value;
  const response = await fetch("/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_url: videoUrl,
      download_type: downloadType,
      quality: quality,
    }),
  });
  StartDownloadPolling();
  DisplayDownloadStarted();
  const data = await response.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  console.log(data);
}

function StartDownloadPolling() {
  downloadInterval = setInterval(() => {
    GetDownloadProgress();
  }, 1000);
}

function StopDownloadPolling() {
  clearInterval(downloadInterval);
  console.log("Polling stopped");

  progressNumber.textContent = "";
  progressMessage.textContent = "Download completed";
}

function GetDownloadProgress() {
  fetch("/progress").then((response) => {
    response.json().then((data) => {
      console.log(data);

      SetProgressBar(data.progress);
      progressNumber.textContent =
        "Download: " + data.progress + "%";
      progressMessage.textContent = data.message;
      //AddMessageLog(data.message);
      if (data.task_complete) {
        console.log("Task completed");
        downloadLink.href = data.download_url;
        StopDownloadPolling();
        DisplayDownloadCompleted();
        return;
      }
    });
  });
}

function SetProgressBar(progress) {
  const progressBar =
    document.getElementById("progressBar");
  progressBar.style.width = `${progress}%`;
}

function AddMessageLog(message) {
  const messageLog = document.getElementById("console-log");
  const messageElement = document.createElement("p");
  messageElement.textContent = message;
  messageLog.appendChild(messageElement);
}

function DisplayPreDownload() {
  document.getElementById("pre-download").style.display =
    "block";
  document.getElementById(
    "download-started"
  ).style.display = "none";
  document.getElementById(
    "download-completed"
  ).style.display = "none";
  SetProgressBar(0); // Make sure it is back to 0
}
function DisplayDownloadStarted() {
  document.getElementById("pre-download").style.display =
    "none";
  document.getElementById(
    "download-started"
  ).style.display = "block";
  document.getElementById(
    "download-completed"
  ).style.display = "none";
}
function DisplayDownloadCompleted() {
  document.getElementById("pre-download").style.display =
    "none";
  document.getElementById(
    "download-started"
  ).style.display = "none";
  document.getElementById(
    "download-completed"
  ).style.display = "block";
}
