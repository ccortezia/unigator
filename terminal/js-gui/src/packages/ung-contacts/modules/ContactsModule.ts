import { Module } from 'vuex';

const ContactsModule = {
    namespaced: true,

    mutations: {
        create(state: any, payload: any) {
            // console.log(payload);
        },
    },
};

export default ContactsModule;
