// Check if documents are stored in local storage
var storedAadharCard = localStorage.getItem('aadharCard');
var storedPanCard = localStorage.getItem('panCard');
var storedDrivingLicense = localStorage.getItem('drivingLicense');

if (storedAadharCard) {
  document.getElementById('aadharCardImage').src = storedAadharCard;
}

if (storedPanCard) {
  document.getElementById('panCardImage').src = storedPanCard;
}

if (storedDrivingLicense) {
  document.getElementById('drivingLicenseImage').src = storedDrivingLicense;
}

function saveDocuments() {
  var aadharFile = document.getElementById('aadharCard').files[0];
  var panFile = document.getElementById('panCard').files[0];
  var drivingLicenseFile = document.getElementById('drivingLicense').files[0];

  // Check if files are selected
  if (aadharFile && panFile && drivingLicenseFile) {
    // Resize and display Aadhar Card image
    var aadharReader = new FileReader();
    aadharReader.onload = function(e) {
      var aadharImg = document.getElementById('aadharCardImage');
      aadharImg.src = e.target.result;
      aadharImg.onload = function() {
        var resizedImg = resizeImage(aadharImg, 200, 200);
        saveToLocalStorage('aadharCard', resizedImg.src);
      };
    };
    aadharReader.readAsDataURL(aadharFile);

    // Resize and display PAN Card image
    var panReader = new FileReader();
    panReader.onload = function(e) {
      var panImg = document.getElementById('panCardImage');
      panImg.src = e.target.result;
      panImg.onload = function() {
        var resizedImg = resizeImage(panImg, 200, 200);
        saveToLocalStorage('panCard', resizedImg.src);
      };
    };
    panReader.readAsDataURL(panFile);

    // Resize and display Driving License image
    var drivingLicenseReader = new FileReader();
    drivingLicenseReader.onload = function(e) {
      var drivingLicenseImg = document.getElementById('drivingLicenseImage');
      drivingLicenseImg.src = e.target.result;
      drivingLicenseImg.onload = function() {
        var resizedImg = resizeImage(drivingLicenseImg, 200, 200);
        saveToLocalStorage('drivingLicense', resizedImg.src);
      };
    };
    drivingLicenseReader.readAsDataURL(drivingLicenseFile);
  } else {
    // Display error message if any file is missing
    alert("Please select Aadhar Card, PAN Card, and Driving License!");
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
