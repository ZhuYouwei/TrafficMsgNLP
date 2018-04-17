var request = require('request')
var moment = require('moment')

/*
	request(url,cb(err,res,body))
*/
var COUNT = 10
var RES = []
var day = 1
var month = 1
function get_ids(page_num,day,month){
	
	var main_url = "http://ogcmn.one.gov.hk/ogcmn/service/list/catwc/OGCMN020*?max=10&page=" + page_num
	// request indexing page get id
	return new Promise(function(resolve, reject) {
		request(main_url, function (error, response, body) {	
			var data_tmp2 = get_item([{'key':"notifications"}],body)
			//console.log(data_tmp2[0]["id"])
			ids = []
			for (var i = 0; i < data_tmp2.length; i++){
				var id = data_tmp2[i]["id"]
				ids.push(id)
			}
			return resolve(ids)
		})
	})
}

function get_detail(id){
	var url = "http://ogcmn.one.gov.hk/ogcmn/service/noti/detail/" + id
	return new Promise(function(resolve, reject) {
		request(url, function (error, response, body) {	
			let data_time = get_item([{'key':"schedule_ts"}],body)
			let data_traffic = get_item([{'key':"msg_en"},{'key':"body"},{'ary':0},{'key':"val"}],body)
			let result = {}
			if (moment(data_time).date() == day && moment(data_time).month() == month - 1){
				result.date = moment(data_time).format("DD-MM H:mm")
				result.msg = data_traffic
				return resolve(result)
			}
			return resolve(null)

		})
	})


}

function get_day(d,m){
	COUNT = 0
	RES = []
	ids = []
	is = [0,1,2,3]
	day = d
	month = m
	var promises = is.map(get_ids)
	return Promise.all(promises)
	    .then(function(res) {
	        ids = [].concat.apply([],res)
	        var promises = ids.map(get_detail)
	        return Promise.all(promises)
	    }).then(function(res){
	    	var r = res.filter(function(x) {
	    	   return x != null;
	    	})
	    	return new Promise(function(resolve, reject){resolve(r)})   	
	    })
}
function get_item(ary,str){
	/*
	[{key: "key_number"},{"ary":index}]
	*/
	var end_index = str.lastIndexOf(")")
	var start_index = str.indexOf("(")
	str = str.substring(start_index + 1, end_index )
	
	for (i = 0; i < ary.length; i ++){
		if ('key' in ary[i]) {
			//console.log(ary[i]['key'],typeof str,str)
			if (typeof str === 'string') {
				var tmp = JSON.parse(str)
				str = tmp[ary[i]['key']]
			} else {
				str = str[ary[i]['key']]
			}
			
		} else {
			str = str[ary[i]['ary']]
		}
	}
	return str
}

module.exports.get_day = get_day

