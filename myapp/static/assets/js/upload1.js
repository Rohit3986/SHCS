// Check if documents are stored in local storage
var storedPrescriptionReport = localStorage.getItem('prescriptionReport');
var storedDiagnosticReport = localStorage.getItem('diagnosticReport');

if (storedPrescriptionReport) {
  document.getElementById('prescriptionReportImage').src = storedPrescriptionReport;
}

if (storedDiagnosticReport) {
  document.getElementById('diagnosticReportImage').src = storedDiagnosticReport;
}

function saveDocuments() {
  var prescriptionReportFile = document.getElementById('prescriptionReport').files[0];
  var diagnosticReportFile = document.getElementById('diagnosticReport').files[0];

  // Check if files are selected
  if (prescriptionReportFile && diagnosticReportFile) {
    // Resize and display Prescription Report image
    var prescriptionReportReader = new FileReader();
    prescriptionReportReader.onload = function(e) {
      var prescriptionReportImg = document.getElementById('prescriptionReportImage');
      prescriptionReportImg.src = e.target.result;
      prescriptionReportImg.onload = function() {
        var resizedPrescriptionReport = resizeImage(prescriptionReportImg, 200, 200);
        saveToLocalStorage('prescriptionReport', resizedPrescriptionReport.src);
      };
    };
    prescriptionReportReader.readAsDataURL(prescriptionReportFile);

    // Resize and display Diagnostic Report image
    var diagnosticReportReader = new FileReader();
    diagnosticReportReader.onload = function(e) {
      var diagnosticReportImg = document.getElementById('diagnosticReportImage');
      diagnosticReportImg.src = e.target.result;
      diagnosticReportImg.onload = function() {
        var resizedDiagnosticReport = resizeImage(diagnosticReportImg, 200, 200);
        saveToLocalStorage('diagnosticReport', resizedDiagnosticReport.src);
      };
    };
    diagnosticReportReader.readAsDataURL(diagnosticReportFile);
  } else {
    // Display error message if any file is missing
    alert("Please select Prescription Report and Diagnostic Report!");
  }
}

function resizeImage(img, maxWidth, maxHeight) {
  var ratio = 1;
  var width = img.width;
  var height = img.height;

  if (width > maxWidth) {
    ratio = maxWidth / width;
    width = maxWidth;
    height = height * ratio;
  }

  if (height > maxHeight) {
    ratio = maxHeight / height;
    height = maxHeight;
    width = width * ratio;
  }

  img.width = width;
  img.height = height;

  return img;
}

function saveToLocalStorage(key, value) {
  localStorage.setItem(key, value);
}
