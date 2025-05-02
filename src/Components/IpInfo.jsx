import React, { useEffect, useState } from 'react';
import axios from 'axios';
import dayjs from "dayjs";

function IpInfo() {
  let [ipData, setIpData] = useState('');
  let [ipconfig, setIpconfig] = useState('');
  let [reqHeaders, setReqHeaders] = useState();
  let [resHeaders, setResHeaders] = useState();

  const timeElapsed = Date.now();
  const today = new Date(timeElapsed);
  let day = today.toDateString()
  let time = today.toUTCString()


const [runningTime, setRunningTime] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setRunningTime(dayjs().format("ddd, D MMM YYYY hh:mm ZZ"));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/')
      .then(response => {
        console.log('axios_response:', response)
        setIpData(response.data.ip);
      })
      .catch(error => {
        setIpData(`Error: ${error.message}`);
      });
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/ipconfig')
      .then(res => {
        console.log('axios_response:', res.data.output)
        setIpconfig(res.data.output);
      })
      .catch(error => {
        setIpconfig(`Error: ${error.message}`);
      });
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/requestheaders')
      .then(res => {
        console.log('@@ Request Headers: ', res.data)
        setReqHeaders(res.data.Date)
      })
      .catch(err => {
        console.error(err)
      })
    }, [])

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/responseheaders')
      .then(res => {
        console.log('## Response Headers: ', res.data)
        setResHeaders(res.data.Date);
      })
      .catch(err => {
        console.error(err);
      });
  }, []);


  return (
    <div>
      <b><h2>현재시간</h2></b>
      <p>{runningTime}</p>
      <br></br>
      <b><h2>IP 정보</h2></b>
      <p>IPV6: {ipData}</p>
      <p>IPV4: {ipconfig}</p>
      <br></br>
      <b><h3>Headers</h3></b>
      <p>Request Headers Date Time: {JSON.stringify(reqHeaders)}</p>
      <p>Response Headers Date Time: {JSON.stringify(resHeaders)}</p>
    </div>
  );
};

export default IpInfo;