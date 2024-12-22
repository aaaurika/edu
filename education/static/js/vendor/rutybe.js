// Функция для воспроизведения видео
function playVideo(videoId) {
    // Скрываем миниатюру и показываем видео
    const thumbnail = document.querySelector(`#${videoId}`).previousElementSibling;
    thumbnail.style.display = 'none';
    document.getElementById(videoId).style.display = 'block';
}
