import Vue from 'vue'
import VueRouter from 'vue-router'

import Cookies from 'js-cookie'

import GetTextPlugin from 'vue-gettext'
import Multiselect from 'vue-multiselect'
import flatpickr from 'flatpickr'
import VueFlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import VuejsDialog from 'vuejs-dialog'
import Notifications from 'vue-notification'
import Acl from './tools/permissions'

import App from './App.vue'
import router from './router'
import store from './store'
import translations from './translations.json'

import Calendar from './components/Calendar.vue'
import Modal from './components/Modal.vue'

import 'vuejs-dialog/dist/vuejs-dialog.min.css'

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
Vue.use(VuejsDialog)
Vue.use(Notifications)
Vue.use(Acl)

/* Configure flatpick widget */
if (userLang !== 'en') {
    import(`flatpickr/dist/l10n/${userLang}.js`).then((locale) => {
        flatpickr.localize(locale.default[userLang])
    })
}
Vue.use(VueFlatPickr)

Vue.component('calendar', Calendar)
Vue.component('modal', Modal)
Vue.component('multiselect', Multiselect)

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
const csrftoken = Cookies.get('csrftoken')
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken

// eslint-disable-next-line no-new
new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store
})
