import Vue from 'vue'
import activities from '../../api/activities'

/**
 * @type {{activities: Array}}
 */
const state = {
    // array of activities
    activities: []
};

/**
 * @type {{get_activities(*=): *, post_activity(*=, *=): *, get_activity(*=, *=): *, delete_activity(*=, *=): *}}
 */
const actions = {
    /**
     * Return a list of Activities
     *
     * @param context
     * @returns {Promise<any>}
     */
    get_activities (context) {
        return new Promise((resolve, reject) => {

            if (context.getters['activities'].length > 0) {
                resolve();
                return;
            }

            activities.activities_get()
                .then((response) => {
                    response.forEach((activity) => {
                        context.commit('ADD_ACTIVITY', activity);
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post a new Activity
     *
     * @param context
     * @param activity
     * @returns {Promise<any>}
     */
    post_activity(context, activity) {
        return new Promise((resolve, reject) => {
            activities.activities_post(activity)
                .then((activity) => {
                    context.commit('ADD_ACTIVITY', activity);
                    resolve(activity);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the Activity identified by the supplied activity_id
     *
     * @param context
     * @param activity_id
     * @returns {Promise<any>}
     */
    get_activity(context, activity_id) {
        return new Promise((resolve, reject) => {
            activities.activity_get(activity_id)
                .then((activity) => {
                    context.commit('ADD_ACTIVITY', activity);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Update an Activity
     *
     * @param context
     * @param activity
     * @returns {Promise<any>}
     */
    put_activity (context, activity) {
        return new Promise((resolve, reject) => {
            activities.activity_put(activity)
                .then((activity) => {
                    context.commit('ADD_ACTIVITY', activity);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Delete an Activity from the Store
     *
     * @param context
     * @param activity
     * @returns {Promise<any>}
     */
    delete_activity(context, activity) {
        return new Promise((resolve, reject) => {
            const activity_id = activity.activity_id;
            activities.activity_delete(activity_id)
                .then(() => {
                    context.commit('REMOVE_ACTIVITY', activity);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    }
};

/**
 * @type {{REMOVE_ACTIVITY(*, *): void, ADD_ACTIVITY(*, *=): void}}
 */
const mutations = {
    /**
     * Add an Activity to the Store
     *
     * @param state
     * @param activity
     * @constructor
     */
    ADD_ACTIVITY (state, activity) {
        const activity_id = activity.activity_id;
        const index = state.activities.findIndex((activity) => activity.activity_id === activity_id);

        if (activity.hasOwnProperty('created')) {
            let created = activity.created;
            activity['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (activity.hasOwnProperty('name')) {
            let name = activity.name;
            let initials = name.match(/\b\w/g).join('');

            let colors = [
                'pink', 'purple', 'deep-purple', 'blue', 'light-blue', 'cyan',
                'teal', 'green', 'light-green', 'lime', 'yellow', 'amber', 'orange',
                'deep-orange', 'blue-grey'
            ];
            // @link https://stackoverflow.com/questions/4550505/getting-a-random-value-from-a-javascript-array
            let color = colors[Math.floor(Math.random() * colors.length)];

            activity['color'] = color;
            activity['initials'] = initials;
        }


        if (index >= 0) {
            Vue.set(state.activities, index, activity);
        } else {
            state.activities.push(activity);
        }
    },
    /**
     * Remove the Activity from the Store
     *
     * @param state
     * @param activity
     * @constructor
     */
    REMOVE_ACTIVITY (state, activity) {
        const activity_id = activity.activity_id;
        const index = state.activities.findIndex((activity) => activity.activity_id === activity_id);

        if (index >= 0) {
            state.activities.splice(index, 1)
        }
    },
};

/**
 * @type {{activity: (function(*): function(*): any), activities: (function(*): (Array|getters.activities|(function(*))|{mutations, state, getters, actions, namespaced}))}}
 */
const getters = {
    /**
     * Activities
     *
     * @param state
     * @returns {getters.activities|(function(*))|Array|{mutations, state, getters, actions, namespaced}|default.computed.activities|(function(*): (Array|getters.activities|(function(*))|{mutations, state, getters, actions, namespaced}))}
     */
    activities: (state) => {
        return state.activities;
    },
    /**
     * Activity
     *
     * @param state
     * @returns {function(*): any}
     */
    activity: (state) => (activity_id) => {
        const activities = state.activities.filter((activity) => activity.activity_id === activity_id);
        return (activities.length === 1) ? activities[0] : {activity_id: null, name: null, code: null, description: null, created: null};
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
