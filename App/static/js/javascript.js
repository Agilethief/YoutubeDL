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

// generate any files already downloaded
BuildDownloadsSection();

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

async function GetDownloadedFiles() {
  const response = await fetch("/get_downloadedfiles");
  const data = await response.json();
  console.log(data);
  return data;
}

function ClearDownloadSection() {
  const downloadTable = document.getElementById(
    "download-table"
  );
  while (downloadTable.rows.length > 0) {
    downloadTable.deleteRow(0);
  }
}

async function BuildDownloadsSection() {
  console.log("1 Building downloads section started");
  const files = await GetDownloadedFiles();

  ClearDownloadSection();

  console.log("2 Building downloads section");
  console.log(files);
  if (files === undefined) {
    return;
  }

  const downloadTable = document.getElementById(
    "download-table"
  );

  console.log("3 Building downloads section");
  files.forEach((element) => {
    // element is just the filename
    console.log(element);
    const newRow = downloadTable.insertRow(0); // Insert at the top
    const cell1 = newRow.insertCell(0); // Filename
    const cell2 = newRow.insertCell(1); // Blank
    const cell3 = newRow.insertCell(2); // Action buttons

    cell1.textContent = element;
    cell2.textContent = "";
    const downloadButton = document.createElement("a");
    downloadButton.textContent = "Download";
    downloadButton.href = "download_file/" + element;
    downloadButton.classList.add("btn");
    downloadButton.classList.add("btn-primary");
    cell3.appendChild(downloadButton);

    const deleteButton = document.createElement("a");
    deleteButton.textContent = "Delete";
    deleteButton.href = "delete_file/" + element;
    deleteButton.classList.add("btn");
    deleteButton.classList.add("btn-danger");
    cell3.appendChild(deleteButton);
  });
}

// Will request all files to be downloaded
function DownloadAll() {
  console.log("Downloading all files");
}

// Will request all files to be deleted and reload the page
function DeleteAll() {
  console.log("Deleting all files");
  window.location.href = "/";
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

  BuildDownloadsSection(); // Update display
}
