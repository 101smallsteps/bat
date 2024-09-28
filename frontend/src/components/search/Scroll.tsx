const Scroll = (props: Props) => {
	return(
		<div style={{overflowY: 'scroll', height:'10vh'}}>
			{props.children}
		</div>
	);
}

export default Scroll;