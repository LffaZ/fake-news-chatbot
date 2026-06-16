const themeToggle = document.getElementById('themeToggle');
const THEME_KEY = 'themeMode';
const THEME_TIME_KEY = 'themeModeTime';
const EXPIRE_TIME = 24 * 60 * 60 * 1000; // 24 jam

// Cek data tersimpan saat halaman dibuka
const savedTheme = localStorage.getItem(THEME_KEY);
const savedTime = localStorage.getItem(THEME_TIME_KEY);

if (savedTheme && savedTime) {
    const now = Date.now();

    if (now - Number(savedTime) < EXPIRE_TIME) {
        if (savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
        }
    } else {
        // Hapus cache jika sudah lewat 24 jam
        localStorage.removeItem(THEME_KEY);
        localStorage.removeItem(THEME_TIME_KEY);
    }
}

themeToggle.addEventListener('click', () => {
    const isDarkMode =
        document.documentElement.getAttribute('data-theme') === 'dark';

    if (!isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.textContent = '☀️';

        localStorage.setItem(THEME_KEY, 'dark');
        localStorage.setItem(THEME_TIME_KEY, Date.now());
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeToggle.textContent = '🌙';

        localStorage.setItem(THEME_KEY, 'light');
        localStorage.setItem(THEME_TIME_KEY, Date.now());
    }
});