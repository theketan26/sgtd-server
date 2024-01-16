import * as React from "react";
import Header from "../components/header/Header";
import Main from "../components/main/Main";


function Home(props) {
	return (
		<div className="bg-orange-100">
			<Header />
			<Main />
		</div>
	);
}

export default Home;
