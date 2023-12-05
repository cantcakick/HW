let names = [];
let isOver = false;
while (!isOver) {
    let name = prompt("What is your name? ");
    if (name != null) {
      names.push(name);
    } else {
      isOver = true;
    }
}
for (let i = 0; i < names.length; i++){
  console.log(names[i]);
}