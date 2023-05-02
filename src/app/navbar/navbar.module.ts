import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; // import HttpClientModule
// import { AppComponent } from './app.component';

@NgModule({
//   declarations: [NavbarComponent],
  imports: [BrowserModule, HttpClientModule], // add HttpClientModule to imports array
  providers: [],
//   bootstrap: [navbarComponent]
})
export class NavbarModule { }
