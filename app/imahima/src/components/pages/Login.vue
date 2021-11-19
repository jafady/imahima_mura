<template>
    <div class="container">
        <div class="position-absolute top-50 start-50 translate-middle">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">ログイン</h5>
                    <form>
                        <div class="mb-3 text-start">
                            <label for="username" class="form-label">名前</label>
                            <input class="form-control" id="username" v-model="credentials.username">
                        </div>
                        <div class="mb-3 text-start">
                            <label for="password" class="form-label">パスワード</label>
                            <input type="password" class="form-control" id="password" v-model="credentials.password">
                        </div>
                        <button type="lohin" class="btn btn-primary" @click="login">ログイン</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="alert alert-warning alert-dismissible fade" v-bind:class="{show: isError}" role="alert">
            ユーザー名かパスワードが間違っています
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data: () => ({
            credentials: {},
            valid:true,
            loading:false,
            isError: false,
            rules:{
                username: [
                    v => !!v || "ユーザー名は必須です",
                ],
                password: [
                    v => !!v || "パスワードは必須です",
                ]
            }
        }
    ),
    methods: {
        login() {
            this.loading = true;
            const userId = this.credentials.username;
            this.$http.post('http://localhost:8000/auth/', this.credentials).then(response => {
                this.$store.dispatch("auth", {
                    userId: userId,
                    userToken: response.data.token
                });
                this.$router.push(this.$route.query.redirect);
            }).catch(e => {
                    this.loading = false;
                    this.isError = true;
            });
        }
    }
}
</script>

<style>
</style>
