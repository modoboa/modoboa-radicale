import Vue from 'vue'
import Router from 'vue-router'

import Calendar from '@/components/Calendar.vue'
import EventForm from '@/components/EventForm.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Calendar',
            component: Calendar
        },
        {
            path: '/:calendar_pk([0-9]+)/:calendar_type(shared|user)/events/:pk([A-Za-z0-9\\-.@]+)/edit',
            name: 'EditEvent',
            component: EventForm
        }
    ],
    linkActiveClass: 'active'
})
