document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function createAppsDropdown() {
        const dropdownContainer = document.createElement('div');
        dropdownContainer.className = 'dropdown-container apps-dropdown';

        const dropdownButton = document.createElement('a');
        dropdownButton.href = '#';
        dropdownButton.className = 'dropdown-button';
        dropdownButton.innerHTML = `Apps <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>`;
        dropdownContainer.appendChild(dropdownButton);

        const dropdownMenu = document.createElement('div');
        dropdownMenu.className = 'dropdown-menu';
        dropdownContainer.appendChild(dropdownMenu);

        const adminAppListDataElement = document.getElementById('admin_app_list_json');
        if (adminAppListDataElement) {
            try {
                const adminAppList = JSON.parse(adminAppListDataElement.textContent);
                adminAppList.forEach(app => {
                    const appItem = document.createElement('div');
                    appItem.className = 'app-item';

                    const appNameLink = document.createElement('a');
                    appNameLink.href = '#';
                    appNameLink.className = 'app-name-link';
                    appNameLink.textContent = app.name;
                    appItem.appendChild(appNameLink);

                    if (app.models.length > 0) {
                        const modelAccordion = document.createElement('div');
                        modelAccordion.className = 'model-accordion';
                        app.models.forEach(model => {
                            const modelLink = document.createElement('a');
                            modelLink.href = model.url;
                            modelLink.className = 'model-link';
                            modelLink.textContent = model.name;
                            modelAccordion.appendChild(modelLink);
                        });
                        appItem.appendChild(modelAccordion);

                        appNameLink.addEventListener('click', function(event) {
                            event.preventDefault();
                            modelAccordion.classList.toggle('show');
                        });
                    }
                    dropdownMenu.appendChild(appItem);
                });
            } catch (e) {
                console.error('Failed to parse admin_app_list_json:', e);
            }
        }

        dropdownButton.addEventListener('click', function(event) {
            event.preventDefault();
            dropdownMenu.classList.toggle('show');
        });

        window.addEventListener('click', function(event) {
            if (!dropdownContainer.contains(event.target)) {
                dropdownMenu.classList.remove('show');
            }
        });

        return dropdownContainer;
    }

    function createUserDropdown() {
        const dropdownContainer = document.createElement('div');
        dropdownContainer.className = 'dropdown-container user-dropdown';

        const dropdownButton = document.createElement('a');
        dropdownButton.href = '#';
        dropdownButton.className = 'dropdown-button';
        const usernameElement = document.getElementById('username_json');
        let username = 'User';
        if (usernameElement) {
            try {
                username = JSON.parse(usernameElement.textContent);
            } catch (e) {
                console.error('Failed to parse username_json:', e);
            }
        }
        dropdownButton.innerHTML = `${gettext('Welcome, ')}${username} <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>`;
        dropdownContainer.appendChild(dropdownButton);

        const dropdownMenu = document.createElement('div');
        dropdownMenu.className = 'dropdown-menu';
        dropdownContainer.appendChild(dropdownMenu);

        const changePasswordLink = document.createElement('a');
        changePasswordLink.href = '/admin/password_change/';
        changePasswordLink.textContent = gettext('Change password');
        dropdownMenu.appendChild(changePasswordLink);

        const logoutLink = document.createElement('a');
        logoutLink.href = '#';
        logoutLink.textContent = gettext('Log out');
        dropdownMenu.appendChild(logoutLink);

        logoutLink.addEventListener('click', function(event) {
            event.preventDefault();
            const logoutForm = document.createElement('form');
            logoutForm.method = 'post';
            logoutForm.action = `/${document.documentElement.lang}/admin/logout/`;
            
            const csrfTokenInput = document.createElement('input');
            csrfTokenInput.type = 'hidden';
            csrfTokenInput.name = 'csrfmiddlewaretoken';
            const existingCsrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            if (existingCsrfInput) {
                csrfTokenInput.value = existingCsrfInput.value;
            } else {
                console.warn('CSRF token input not found. Logout might fail.');
            }
            logoutForm.appendChild(csrfTokenInput);
            
            document.body.appendChild(logoutForm);
            logoutForm.submit();
        });

        dropdownButton.addEventListener('click', function(event) {
            event.preventDefault();
            dropdownMenu.classList.toggle('show');
        });

        window.addEventListener('click', function(event) {
            if (!dropdownContainer.contains(event.target)) {
                dropdownMenu.classList.remove('show');
            }
        });

        return dropdownContainer;
    }

    function createLanguageSelector() {
        const languageSelector = document.createElement('div');
        languageSelector.className = 'language-selector';

        const languageForm = document.createElement('form');
        languageForm.action = '/i18n/setlang/';
        languageForm.method = 'post';
        languageSelector.appendChild(languageForm);

        const csrfTokenInput = document.createElement('input');
        csrfTokenInput.type = 'hidden';
        csrfTokenInput.name = 'csrfmiddlewaretoken';
        csrfTokenInput.value = getCookie('csrftoken');
        languageForm.appendChild(csrfTokenInput);

        const languageInput = document.createElement('input');
        languageInput.type = 'hidden';
        languageInput.name = 'next';

        const languages = [
            { code: 'en', name: 'English', flag: '🇺🇸' },
            { code: 'es', name: 'Español', flag: '🇻🇪' }
        ];

        let currentPath = window.location.pathname;
        // Remove any existing language prefix from the path
        const pathParts = currentPath.split('/');
        if (pathParts.length > 1 && languages.some(lang => lang.code === pathParts[1])) {
            currentPath = '/' + pathParts.slice(2).join('/');
        }
        if (!currentPath.startsWith('/')) {
            currentPath = '/' + currentPath;
        }

        // Function to get the target URL based on selected language
        function getTargetUrl(selectedLangCode) {
            // If the current path is just '/', we want to go to /<lang_code>/
            // Otherwise, prepend the lang code to the current path
            if (currentPath === '/') {
                return `/${selectedLangCode}/`;
            } else {
                return `/${selectedLangCode}${currentPath}`;
            }
        }

        // Initialize the 'next' input value with the current language's admin path
        languageInput.value = getTargetUrl(document.documentElement.lang);
        languageForm.appendChild(languageInput);

        const languageSelect = document.createElement('select');
        languageSelect.name = 'language';
        languageSelect.onchange = function() {
            const selectedLangCode = this.value;
            languageInput.value = getTargetUrl(selectedLangCode); // Update next URL based on selection
            this.form.submit();
        };
        languageForm.appendChild(languageSelect);

        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.flag;
            if (lang.code === document.documentElement.lang) {
                option.selected = true;
            }
            languageSelect.appendChild(option);
        });

        return languageSelector;
    }

    function createThemeToggle() {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = `
            <span class="visually-hidden theme-label-when-light">Toggle theme (current theme: light)</span>
            <span class="visually-hidden theme-label-when-dark">Toggle theme (current theme: dark)</span>
            <svg aria-hidden="true" class="theme-icon-when-dark">
                <use xlink:href="#icon-moon" />
            </svg>
            <svg aria-hidden="true" class="theme-icon-when-light">
                <use xlink:href="#icon-sun" />
            </svg>
        `;
        return themeToggle;
    }

    const customNavbarContainer = document.getElementById('custom-navbar-container');
    if (customNavbarContainer) {
        // Append new elements directly to the container
        customNavbarContainer.appendChild(createUserDropdown());
        customNavbarContainer.appendChild(createLanguageSelector());
        customNavbarContainer.appendChild(createThemeToggle()); // Re-create the theme toggle
    }

    // Add a class to the body if on the login page
    if (window.location.pathname.includes('/admin/login')) {
        document.body.classList.add('login-page');
    }
});