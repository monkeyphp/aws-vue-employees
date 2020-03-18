/**
 * @file activities.js
 */
/* eslint-disable */
import axios from 'axios';

export default {
    /**
     * Return a list of Activities
     *
     * @returns {Promise<any>}
     */
    activities_get() {
        return new Promise((resolve, reject) => {
            axios.get('/activities')
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                })
        });
    },
    /**
     * Post an Activity to the api
     *
     * @param activity
     * @returns {Promise<any>}
     */
    activities_post(activity) {
        return new Promise((resolve, reject) => {
            axios.post('/activities', activity)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        })
    },
    /**
     * Return the Activity identified by the supplied activity_id
     *
     * @param activity_id
     * @returns {Promise<any>}
     */
    activity_get(activity_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/activities/${activity_id}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Update the Activity
     *
     * @param activity
     * @returns {Promise<any>}
     */
    activity_put (activity) {
        console.log(activity);
        return new Promise((resolve, reject) => {
            const activity_id = activity.activity_id;
            axios.put(`/activities/${activity_id}`, activity)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Delete the Activity identified by the supplied activity_id
     *
     * @param activity_id
     * @returns {Promise<any>}
     */
    activity_delete(activity_id) {
        return new Promise((resolve, reject) => {
            axios.delete(`/activities/${activity_id}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    }
};