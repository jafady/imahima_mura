import { createStore } from 'vuex'

export default createStore({
  state: {
    userId: "",
    userToken: ""
  },
  mutations: {
    updateUser(state, user) {
      state.userId = user.userId;
      state.userToken = user.userToken;
    }
  },
  actions: {
    auth(context, user) {
      context.commit('updateUser', user);
    }
  },
  modules: {
  }
})
