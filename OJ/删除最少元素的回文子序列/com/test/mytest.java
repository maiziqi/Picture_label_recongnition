package com.test;
public class mytest{
	private class Node{
		public int drop_num;
		public boolean flag;
		public Node(int drop_num,boolean flag){
			this.drop_num=drop_num;
			this.flag=flag;
		}
	}
	private String str;
	private Node[][] node;
	private int len;
	public mytest(String str){
		this.str=str;
		this.len=str.length();
		this.node=new Node[len][len];
	}
	public static void main(String[] args){
		String str="aebccbea";
		mytest mt=new mytest(str);
		for(int l=0;l<=mt.len-2;l++){
			for(int i=0;i<=l;i++){
				int j=l-i;
				mt.judgeDrop_num(i,j);
			}
		}
		int min=mt.len;
		for(int i=0;i<=mt.len-2;i++){
			int j=mt.len-2-i;
			int curr_result=mt.node[i][j].drop_num;
			if(!mt.node[i][j].flag) curr_result++;
			if(curr_result<min) min=curr_result;
		}
		System.out.println(min);
	}
	void judgeDrop_num(int i,int j){
		//one																		//		one|two
		int one=i+j,two=i+j,thr=i+j;		//i+j肯定是最大的						//		thr|cur
		if(isexist(i-1,j-1)&&node[i-1][j-1].flag){
			one=node[i-1][j-1].drop_num;
		}
		//two
		if(isexist(i-1,j)){
			two=node[i-1][j].drop_num+1;
		}
		//thr
		if(isexist(i,j-1)){
			thr=node[i][j-1].drop_num+1;
		}
		node[i][j]=new Node(get_min(one,two,thr),judgeFlag(i,j));
		System.out.printf("i:%d,j:%d,num:%d,flag:%b\n",i,j,node[i][j].drop_num,node[i][j].flag);
		// return get_min(one,two,thr);
	}
	boolean judgeFlag(int i,int j){
		if(str.charAt(i)==str.charAt(len-j-1)) return true;
		return false;
	}
	boolean isexist(int i,int j){
		if(i<0||j<0){
			return false;
		}
		return true;
	}
	int get_min(int a,int b,int c){
		if(a>b) a=b;
		if(a>c) a=c;
		return a;
	}
}