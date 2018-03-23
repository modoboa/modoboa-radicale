import Vue from 'vue'
import VueRouter from 'vue-router'

import Cookies from 'js-cookie'
import moment from 'moment'

import GetTextPlugin from 'vue-gettext'
import Multiselect from 'vue-multiselect'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import VuejsDialog from 'vuejs-dialog'
import Notifications from 'vue-notification'

import App from './App.vue'
import router from './router'
import store from './store'
import translations from './translations.json'

import Calendar from './components/Calendar.vue'

Vue.use(GetTextPlugin, {
    availableLanguages: {
        en: 'English',
        fr: 'Français'
    },
    translations: translations
})
/* global userLang */
Vue.config.language = userLang

Vue.use(VueRouter)
Vue.use(flatPickr)
Vue.use(VuejsDialog)
Vue.use(Notifications)

Vue.component('calendar', Calendar)
Vue.component('multiselect', Multiselect)

Vue.filter('formatDate', (value, format) => {
    if (value) {
        return moment(String(value)).format(format || 'MM/DD/YYYY hh:mm')
    }
})

/* Global event bus */
const EventBus = new Vue()

Object.defineProperties(Vue.prototype, {
    $bus: {
        get: function () {
            return EventBus
        }
    }
})

/* Deal with django CSRF protection */
let csrftoken = Cookies.get('csrftoken')
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken

// eslint-disable-next-line no-new
new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store
})
