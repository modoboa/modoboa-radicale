import Vue from 'vue'
import VueRouter from 'vue-router'

import Cookies from 'js-cookie'
import moment from 'moment'
import GetTextPlugin from 'vue-gettext'

import App from './App.vue'
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

Vue.component('calendar', Calendar)

Vue.filter('formatDate', (value, format) => {
    if (value) {
        return moment(String(value)).format(format || 'MM/DD/YYYY hh:mm')
    }
})

let csrftoken = Cookies.get('csrftoken')
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken

const routes = [

]

export var router = new VueRouter({
    routes,
    linkActiveClass: 'active'
})

// eslint-disable-next-line no-new
new Vue({
    el: '#app',
    render: h => h(App),
    router
})
