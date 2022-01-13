import axios from 'axios';
import getConfig from 'next/config';

const { publicRuntimeConfig } = getConfig();

axios.defaults.withCredentials = true;
axios.defaults.baseURL = publicRuntimeConfig.BACKEND_BASE_URL;
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.xsrfCookieName = 'X-CSRF-Token';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const axiosInstance = axios.create();

// axiosInstance.interceptors.request.use();

export default axiosInstance;
