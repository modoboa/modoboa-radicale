import Vue from 'vue'
import Vuex from 'vuex'

import calendar from './modules/calendar'
import event from './modules/event'

Vue.use(Vuex)

const options = {
    modules: {
        calendar,
        event
    },
    strict: process.env.NODE_ENV !== 'production'
}

export default new Vuex.Store(options)
export { options }
