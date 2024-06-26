document.addEventListener('DOMContentLoaded', function () {
    const videoContainers = document.querySelectorAll('.video-container');

    videoContainers.forEach((container, index) => {
        const videoPlayer = container.querySelector('video');
        const annotations = container.querySelectorAll('.annotation');
        const caption = container.querySelector('.caption');
        const speedControl = container.querySelector('.speed-control');

        const projectName = window.location.pathname.split('/')[2];

        speedControl.addEventListener('change', function () {
            videoPlayer.playbackRate = parseFloat(speedControl.value);
        });

        annotations.forEach(annotation => {
            const start = parseFloat(annotation.getAttribute('data-start'));
            const end = parseFloat(annotation.getAttribute('data-end'));
            const label = annotation.querySelector('p').textContent;
            const correctButton = annotation.querySelector('.correct');
            const incorrectButton = annotation.querySelector('.incorrect');

            videoPlayer.addEventListener('timeupdate', function () {
                if (videoPlayer.currentTime >= start && videoPlayer.currentTime <= end) {
                    caption.textContent = label;
                    caption.style.display = 'block';
                    correctButton.disabled = false;
                    incorrectButton.disabled = false;
                } else if (videoPlayer.currentTime > end) {
                    caption.style.display = 'none';
                    correctButton.disabled = true;
                    incorrectButton.disabled = true;
                }
            });

            correctButton.addEventListener('click', function () {
                fetch(`/log_label/${projectName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        video: videoPlayer.querySelector('source').src,  // Correctly retrieve video source URL
                        start: start,
                        end: end,
                        label: label,
                        status: 'correct'
                    })
                });
                annotation.style.display = 'none';
            });

            incorrectButton.addEventListener('click', function () {
                fetch(`/log_label/${projectName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        video: videoPlayer.querySelector('source').src,  // Correctly retrieve video source URL
                        start: start,
                        end: end,
                        label: label,
                        status: 'incorrect'
                    })
                });
                annotation.style.display = 'none';
            });
        });
    });
});
