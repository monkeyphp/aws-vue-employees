import Vue from 'vue'
import Vuex from 'vuex'

import employees from './modules/employees'
import groups from './modules/groups'
import activities from './modules/activities'

Vue.use(Vuex);

// const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    modules: {
        activities,
        employees,
        groups,
    },
    strict: true,
    plugins: []
})