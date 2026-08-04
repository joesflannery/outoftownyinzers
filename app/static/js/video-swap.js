// Clicking a secondary video thumbnail swaps it into the main embed (and
// plays it) instead of navigating away to YouTube -- the outgoing main
// video takes that thumbnail's spot in the row below.
document.addEventListener("DOMContentLoaded", function () {
    var iframe = document.getElementById("main-video-iframe");
    var boxRow = document.getElementById("video-box-row");
    if (!iframe || !boxRow) return;

    boxRow.querySelectorAll(".video-box").forEach(function (box) {
        box.addEventListener("click", function (event) {
            event.preventDefault();

            var newId = box.dataset.videoId;
            var newTitle = box.dataset.videoTitle;

            var oldId = iframe.dataset.videoId;
            var oldTitle = iframe.dataset.videoTitle;
            var oldThumbnail = iframe.dataset.videoThumbnail;

            iframe.src = "https://www.youtube.com/embed/" + newId + "?autoplay=1";
            iframe.title = newTitle;
            iframe.dataset.videoId = newId;
            iframe.dataset.videoTitle = newTitle;
            iframe.dataset.videoThumbnail = box.dataset.videoThumbnail;

            box.href = "https://www.youtube.com/watch?v=" + oldId;
            box.dataset.videoId = oldId;
            box.dataset.videoTitle = oldTitle;
            box.dataset.videoThumbnail = oldThumbnail;

            var img = box.querySelector("img");
            if (img) {
                img.src = oldThumbnail;
                img.alt = oldTitle;
            }
            var titleEl = box.querySelector(".video-box-title");
            if (titleEl) {
                titleEl.textContent = oldTitle;
            }
        });
    });
});
