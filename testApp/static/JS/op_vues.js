(function () {
    "user strict"
    const OPHandling2 = {
        data() {
            return {
                ops: []
            }
        },
        methods: {
            request2(e) {
                
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

                axios({
                    method: 'GET',
                    url: 'http://127.0.0.1:8000/api/v1/mstData/opportunity',
                    responseType: 'json'
                }).then(response => this.ops = response.data["results"]).catch(error => console.log(error))
            }
        },
        delimiters: ['[[', ']]']
    }

    Vue.createApp(OPHandling2).mount('#list-rendering')


    const OPHandling1 = {
        data() {
            return {
                hoge: "a"
            }
        },
        methods: {
            request1(e) {
                
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

                axios({
                    method: 'GET',
                    url: 'http://127.0.0.1:8000/api/v1/mstData/opportunity',
                    responseType: 'json'
                }).then(response => OPHandling2.ops = response.data["results"]).catch(error => console.log(error))

                
            }
        },
        delimiters: ['[[', ']]']
    }

    Vue.createApp(OPHandling1).mount('#bottom_nav')
    
    OPHandling2.ops = ["aa"]
    
})();