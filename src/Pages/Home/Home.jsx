import React from 'react';
import LogoutButton from '../../Components/LogoutButton/LogoutButton';


function Home() {
  return(
    <>
    <div>
      HOME - You are logged in!
    </div>
    <div>
      <LogoutButton />
    </div>
    </>
  )
}

export default Home;