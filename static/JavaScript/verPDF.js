var url = document.getElementById("pdf-url").value;
var pdfDoc = null;
var currentPage = 1;
var totalPages = 0;

function loadPDF(url) {
  totalPages = 0;
  currentPage = 1;

  pdfjsLib.getDocument(url).promise.then(function (pdfDoc_) {
    pdfDoc = pdfDoc_;
    totalPages = pdfDoc.numPages;
    document.getElementById("page-count").textContent = totalPages;
    renderPage(currentPage);
  });
}

function renderPage(pageNum) {
  pdfDoc.getPage(Number(pageNum)).then(function (page) {
    var scale = 1.5;
    var viewport = page.getViewport({ scale: scale });

    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");
    canvas.width = viewport.width;
    canvas.height = viewport.height;

    page.render({
      canvasContext: context,
      viewport: viewport,
    });

    document.getElementById("pdf-container").innerHTML = "";
    document.getElementById("pdf-container").appendChild(canvas);
    document.getElementById("page-num").textContent = currentPage;
  });
}

function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    renderPage(currentPage);
  }
}

function previousPage() {
  if (currentPage > 1) {
    currentPage--;
    renderPage(currentPage);
  }
}
