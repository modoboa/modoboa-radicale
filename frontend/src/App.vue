<template>
  <div id="app">
    <div id="leftcol" class="sidebar collapse navbar-collapse">
      <ul class="nav nav-sidebar" role="menu">
        <li class="nav-header"><translate>My calendars</translate></li>
        <li><a href="#" @click="showCalendarForm = true"><span class="fa fa-plus"></span> <translate>New calendar</translate></a></li>
        <li v-for="calendar in calendars" class="dropdown-submenu">
          <a href="#" @click="toggleSubmenu"><span class="square" v-bind:style="{ 'background-color': calendar.color }"></span> {{ calendar.name }}</a>
          <ul class="dropdown-menu">
            <li>
              <a href="#" @click="editCalendar(calendar.pk)">
                <span class="fa fa-edit"></span> <translate>Edit calendar</translate>
              </a>
            </li>
            <li>
              <a href="#" @click="editCalendarAccessRules(calendar.pk)">
                <span class="fa fa-filter"></span> <translate>Access rules</translate>
              </a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="main">
      <calendar :eventSources="eventSources" :locale="locale"></calendar>
    </div>

    <calendar-form v-if="showCalendarForm" :pk="currentCalendarPk" :show.sync="showCalendarForm"></calendar-form>

    <calendar-accessrules-form v-if="showAccessRulesForm" :show.sync="showAccessRulesForm"></calendar-accessrules-form>
  </div>
</template>

<script>
 import $ from 'jquery'
 import * as api from './api'
 import CalendarForm from './components/CalendarForm.vue'
 import CalendarAccessRulesForm from './components/CalendarAccessRulesForm.vue'
 
 export default {
     components: {
         'calendar-form': CalendarForm,
         'calendar-accessrules-form': CalendarAccessRulesForm
     },
     data () {
         return {
             calendars: [],
             eventSources: ['/api/v1/events/'],
             locale: this.$language.current,
             showCalendarForm: false,
             showAccessRulesForm: false
         }
     },
     created () {
         this.getCalendars()
     },
     methods: {
         getCalendars () {
             api.getUserCalendars().then(response => {
                 this.calendars = response.data
             })
         },
         editCalendar (pk) {
             this.currentCalendarPk = pk
             this.showCalendarForm = true
         },
         editCalendarAccessRules (pk) {
             this.showAccessRulesForm = true
         },
         toggleSubmenu (e) {
             $(e.target).next('ul').toggle()
         }
     }
 }
</script>

<style>
 .square {
     display: inline-block;
     border-color: #ddd;
     border-radius: 1px;
     margin-right: 4px;
     height: 11px;
     width: 11px;
 }

 .dropdown-submenu {
     position: relative;
 }

 .dropdown-submenu .dropdown-menu {
     top: 0;
     left: 100%;
     margin-top: -1px;
 }
</style>
