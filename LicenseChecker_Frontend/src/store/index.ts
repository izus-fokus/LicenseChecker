// index.js (Vuex store)
import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({ // store setup
    state: { // hold data to share accross the app
        selectedOption: 'github', // Default selected option
        showDiv1: true, // Initial state for showDiv1
        licenses: null, // Initial state for licenses

    },
    mutations: { // commit mutations to modify the state
        setSelectedOption(state, option) {
            state.selectedOption = option;
        },
        setShowDiv1(state, show) {
            state.showDiv1 = show;
        },
        setLicenses(state, licenses) {
            state.licenses = licenses;
        },

    },
    actions: { // it set the values in mutation,(commit mutations to modify the state.)
        updateSelectedOption({ commit }, option) {
            commit('setSelectedOption', option);
        },
        updateShowDiv1({ commit }, show) {
            commit('setShowDiv1', show);
        },
        updateLicenses({ commit }, licenses) {
            commit('setLicenses', licenses);
        },


    },
    getters: {
        getSelectedOption: (state) => state.selectedOption,
        getShowDiv1: (state) => state.showDiv1,
        getLicenses: (state) => state.licenses,

    },

});
